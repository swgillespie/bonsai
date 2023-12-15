`bonsai down` on the tip of a two-commit stack:

  $ git init
  Initialized empty Git repository in /tmp/tempdir/.git/
  $ echo a > a.txt
  $ git add a.txt
  $ git commit -m "1" --quiet
  $ git checkout -b feature
  !Switched to a new branch 'feature'
  $ echo b > b.txt
  $ git add b.txt
  $ git commit -m "2" --quiet
  $ git checkout -b feature2
  !Switched to a new branch 'feature2'
  $ echo c > c.txt
  $ git add c.txt
  $ git commit -m "3" --quiet

Should move down one commit in the stack:

  $ git log --pretty=format:%s
  3
  2
  1
  $ python3 -m bonsai down
  $ git log --pretty=format:%s
  2
  1
