Rails.application.routes.draw do
  devise_for :admin_users, ActiveAdmin::Devise.config

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
    ActiveAdmin.routes(self)
  # For details on the DSL available within this file, see http://guides.rubyonrails.org/routing.html
end
