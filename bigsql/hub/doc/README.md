PGCLI is a PrettyGoodCommandLIne interface for component control and management.  

## Usage ##
```
#!
pgc [options] command [component1 [component2 ...] ]
```

## Informational Commands ##
```
#!
  help      - Display help file
  info      - Display OS or component information
  status    - Display status of installed server components
  top       - A cross platform version of the *NIX "top" command 
  list      - Display available/installed components 

```

## Service Control Commands ##
```
#!
  start     - Start server components
  stop      - Stop server components
  reload    - Reload server configuration files (without a restart)
  restart   - Stop & then start server components

  enable    - Enable a component
  disable   - Disable a server server component from starting automatically

  config    - Configure a component
  init      - Initialize a component.  For example
                 ./pgc init pg95 --options "-e utf"


```

## Software Install & Update Commands ##
```
#!
  update    - Retrieve new lists of components
  upgrade   - Perform an upgrade of a component
  install   - Install (or re-install) a component  
  remove    - Un-install component   
  download  - Download a component archive file (but doi not install it)
  clean     - Delete downloaded component files
```

## Advanced Commands & Options ##
```
#!
  get        - Retrieve a Setting.  ie  get GLOBAL REPO
  set        - Populate a Setting.  ie  set GLOBAL REPO "http://localhost:8000"
  unset      - Remove a Setting (very dangerous if you dont know what you are doing) 
  register   - Create a HOST, GROUP or REPO meta data entry
  unregister - Delete a HOST, GROUP or REPO meta data entry
  --host     - Specify a remote HOST for a PGC command
```
