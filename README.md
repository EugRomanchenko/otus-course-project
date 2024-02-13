```commandline
get-content .env.example | foreach {
   $name, $value = $_.split('=')
   set-content env:$name $value
}
cd app/
alembic current

```