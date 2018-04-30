# fitnessapp

> Проект фитнесс приложения

## Build Setup

### Python

```bash
# install dependencies
pip install -r requirements.txt

# initial db
python manage.py db init

# make migrations
python manage.py db migrate

# upgrade database
python manage.py db upgrade

# run dev server (localhost:5000)
python manage.py runserver
```

### Vue.js

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev

# webpack watch (for creating file in static folder)
npm run watch

# build for production with minification
npm run build
```

For detailed explanation on how things work, consult the [docs for vue-loader](http://vuejs.github.io/vue-loader).

### DB
Export from CSV files categories and exercises into DB

### TESTS

```
# run all tests
nosetests

# run only one file
nosetests test/<your-file-here>.py
```

for debug add to end of file
```python
if __name__ == '__main__':
    unittest.main()
```