####################################################################
#########      Copyright (c) 2016-2017 BigSQL           ############
####################################################################

import paramiko
from fabric.state import connections, ssh
from fabric.api import env, hide, cd, put, run, settings, sudo
from fabric.contrib import files
from StringIO import StringIO
from fabric.context_managers import shell_env
import os
from fabric.context_managers import remote_tunnel

class PgcRemoteException(Exception):
    pass


class PgcRemote(object):
    def __init__(self, host, username="", password=""):
        self.user = username
        self.host = host
        self.password = password
        self.sftp = None
        self.client = None
        env.host_string = "%s@%s" % (username, host)  # , 22)
        env.password = password
        env.remote_interrupt = True
        env.output_prefix = False
        env.connection_attempts = 1
        env.warn_only = True

    def connect(self):
        sshClient = ssh.SSHClient()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        sshClient.connect(self.host,
                          username=self.user,
                          password=self.password, timeout=10)
        #if env.host_string not in connections:
        #    connections[env.host_string] = sshClient
        self.client = sshClient

    def has_sudo(self):
        with settings(hide('everything'), warn_only=True):
            cmd="uname"
            m = sudo(cmd, shell_escape=True, pty=False)
            has_root_access=False
            if m.return_code == 0:
                has_root_access=True
            return has_root_access

    def is_exists(self, path):
        return files.exists(path)

    def add_file(self, path, txt):
        files.append(path, txt)

    def has_execution_access(self, path):
        fn = run if not self.has_sudo else sudo
        with settings(hide('everything'), warn_only=True):
            response = fn('test -x ' + path)
            return response.return_code == 0

    def user_exists(self, user):
        """
        Determine if a user exists with given user.

        This returns the information as a dictionary
        '{"name":<str>,"uid":<str>,"gid":<str>,"home":<str>,"shell":<str>}' or 'None'
        if the user does not exist.
        """
        with settings(hide('warnings','stderr','stdout','running'),warn_only=True):
            user_data = run("cat /etc/passwd | egrep '^%s:' ; true" % user)

        if user_data:
            u = user_data.split(":")
            return dict(name=u[0],uid=u[2],gid=u[3],home=u[5],shell=u[6])
        else:
            return None

    def user_create(self, user, home=None, uid=None, gid=None, password=False):
        """
        Creates the user with the given user, optionally giving a specific home/uid/gid.

        By default users will be created without a password.  To create users with a
        password you must set "password" to True.
        """
        u = self.user_exists(user)
        if not u:
            options = []
            if home: options.append("-d '%s'" % home)
            if uid:  options.append("-u '%s'" % uid)
            if gid:  options.append("-g '%s'" % gid)
            if not password: options.append("--disabled-password")
            sudo("adduser %s '%s'" % (" ".join(options), user))
        else:
            return None

    def group_exists(self, name):
        """
        Determine if a group exists with a given name.

        This returns the information as a dictionary
        '{"name":<str>,"gid":<str>,"members":<list[str]>}' or 'None'
        if the group does not exist.
        """
        with settings(hide('warnings','stderr','stdout','running'),warn_only=True):
            group_data = run("cat /etc/group | egrep '^%s:' ; true" % (name))

        if group_data:
            name,_,gid,members = group_data.split(":",4)
            return dict(name=name,gid=gid,members=tuple(m.strip() for m in members.split(",")))
        else:
            return None
        return None

    def group_create(self, name, gid=None):
        """ Creates a group with the given name, and optionally given gid. """
        options = []
        if gid: options.append("-g '%s'" % gid)
        sudo("addgroup %s '%s'" % (" ".join(options), name))

    def group_user_exists(self, group, user):
        """ Determine if the given user is a member of the given group. """
        g = self.group_exists(group)

        u = self.user_exists(user)

        return user in g["members"]

    def group_user_add(self, group, user):
        """ Adds the given user to the given group. """
        if not self.group_user_exists(group, user):
            sudo('adduser %s %s' % (user, group))

    def grant_sudo_access(self, user, service_name):
        """ Grants sudo access to a user. """
        u = self.user_exists(user)
        if u:
          service_cmd = self.get_systemctl_path()
          if service_cmd is None:
            # Not a systemd platform
            service_cmd = "/sbin/service "
            sudo_cmds = [user + " ALL=(ALL) NOPASSWD:" + service_cmd + service_name + " start",
                         user + " ALL=(ALL) NOPASSWD:" + service_cmd + service_name + " stop",
                         user + " ALL=(ALL) NOPASSWD:" + service_cmd + service_name + " restart",
                         user + " ALL=(ALL) NOPASSWD:" + service_cmd + service_name + " status"]
          else:
            sudo_cmds = [user + " ALL=(ALL) NOPASSWD:" + service_cmd + " start "   + service_name,
                         user + " ALL=(ALL) NOPASSWD:" + service_cmd + " stop "    + service_name,
                         user + " ALL=(ALL) NOPASSWD:" + service_cmd + " restart " + service_name,
                         user + " ALL=(ALL) NOPASSWD:" + service_cmd + " status "  + service_name]

          for cmd in sudo_cmds:
            files.append("/etc/sudoers.d/" + user, cmd, use_sudo=True)

    def get_systemctl_path(self):
        systemctls = ["/usr/bin/systemctl", "/bin/systemctl"]
        for pth in systemctls:
            if self.is_exists(pth) and self.has_execution_access(pth):
                return pth
        return None

    def upload_pgc(self, source_path, target_path, pgc_version, repo, repo_port=8000):
        with cd(target_path), shell_env(PGC_VER=pgc_version, PGC_REPO=repo), remote_tunnel(repo_port),hide("everything"):
            pgc_file = "bigsql-pgc-" + pgc_version + ".tar.bz2"
            source_file = os.path.join(source_path, pgc_file)
            put(source_file, ".")
            source_file = os.path.join(source_path, "install.py")
            put(source_file, ".")
            run("python install.py")
            run("rm install.py")

    def execute(self, cmd):
        with settings(hide('everything'), warn_only=True):
            m = run(cmd, shell_escape=True, pty=False)
            if m.return_code == 0:
                out = m.stdout.strip()
                err = m.stderr.strip()
            else:
                out = ""
                err = m.stdout.strip()
            return {"stdout": out, "stderr": err}

    def execute_stream(self, cmd):
        with settings(hide('warnings', 'running', 'stderr'), warn_only=True):
            m = run(cmd, shell_escape=True, pty=False)
            if m.return_code == 0:
                out = m.stdout.strip()
                err = m.stderr.strip()
            else:
                out = ""
                err = m.stdout.strip()
            return {"stdout": out, "stderr": err}

    def disconnect(self):
        host = self.host
        if host and host in connections:
            connections[host].get_transport().close()
        if hasattr(self.client, 'get_transport'):
            self.client.get_transport().close()
