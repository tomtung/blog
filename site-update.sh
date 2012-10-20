# This script syncs the deploy branch with the master branch

git checkout -f deploy
git merge --no-commit master
rake generate
git add public/*

git status
read -p "Press [Enter] to commit to the deploy branch..."
git commit -m "Site updated."
git checkout master