## Udacity Tournament Database Project

### Files 

- tournament.py
- tournament.sql
- tourname_test.py

### Usage

Login to vagrant

```
vagrant up; vagrant ssh
```

Create Database

```
vagrant@vagrant-ubuntu-trusty-32:/vagrant/tournament$ psql
psql (9.3.5)
Type "help" for help.

vagrant=> \i tournament.sql
vagrant=> \q
```

Run all the tests:

```python
python tournament_test.py
```

### License 

MIT