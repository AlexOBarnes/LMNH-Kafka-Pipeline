source .env
export PGPASSWORD=$PASSWORD1
psql -h $HOST -U $USER museum -c "TRUNCATE rating_interaction,request_interaction;"