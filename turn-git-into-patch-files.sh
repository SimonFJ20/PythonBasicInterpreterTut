set -xe
read -p "Repo: SimonFJ20/" repo
git clone "git@github.com:SimonFJ20/$repo"
cd $repo
mkdir -p commits
cd commits/
git rev-list --remotes | xargs -L1 git format-patch -1
cd ..
rm -rf .git
cd ..
echo "Done"

