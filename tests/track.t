`bonsai track` on the tip of a one-commit stack:

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

Should track the feature branch:

  $ python3 -m bonsai track
  Now tracking branch feature
  $ python3 -m bonsai track
  Branch feature is already tracked

