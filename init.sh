# This script needs to be executed after cloning the repository
# to add the "octopress" remote and to set up the "deploy" branch for Heroku

# After executing this script, "git push" on master branch
# pushes to origin/master, while on deploy branch pushes to heroku/master

# To get updates from octpress, manually do "git merge octopress/master"

git remote add octopress https://github.com/imathis/octopress.git
git fetch octopress

git remote add heroku git@heroku.com:tomtung-blog.git
git fetch heroku
git checkout -b deploy heroku/master
git config --local push.default upstream

git checkout master