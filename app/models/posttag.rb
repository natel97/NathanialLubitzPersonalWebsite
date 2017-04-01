class Posttag < ApplicationRecord
  has_one :tag;
  has_one :post;
end
