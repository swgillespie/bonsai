`bn down` on the tip of a two-commit stack:

  $ git init
  $ echo a > a.txt
  $ git add a.txt
  $ git commit -m "1"
  $ git checkout -b feature
  $ echo b > b.txt
  $ git add b.txt
  $ git commit -am "2"
  $ git checkout -b feature2
  $ echo c > c.txt
  $ git add c.txt
  $ git commit -am "3"

Should move down one commit in the stack:

  $ bonsai down
  $ git log --pretty=format:%s