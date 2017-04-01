class CreatePosttags < ActiveRecord::Migration[5.0]
  def change
    create_table :posttags do |t|
      t.integer :tagID
      t.integer :postID

      t.timestamps
    end
  end
end
