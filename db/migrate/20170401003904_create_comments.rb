class CreateComments < ActiveRecord::Migration[5.0]
  def change
    create_table :comments do |t|
      t.integer :UserID
      t.integer :postID
      t.text :content
      t.string :flagged

      t.timestamps
    end
  end
end
