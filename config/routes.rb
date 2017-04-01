Rails.application.routes.draw do
  get 'tags/index'

  get 'tags/edit'

  get 'tags/new'

  get 'tags/show'

  get 'portfolio/portfolio'
  resources :posts
  resources :categories
  resources :tags
  resources :posttags
  resources :comments
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
