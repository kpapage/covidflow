set -e

mongosh <<EOF
db = db.getSiblingDB('admin')
db.auth('$MONGO_INITDB_ROOT_USERNAME', '$MONGO_INITDB_ROOT_PASSWORD')

db = db.getSiblingDB('$MONGO_INITDB_DATABASE')
db.createUser({
  user: '$MONGO_INITDB_ROOT_USERNAME',
  pwd: '$MONGO_INITDB_ROOT_PASSWORD',
  roles: [{ role: 'readWrite', db: '$MONGO_INITDB_DATABASE' }],
});

EOF

echo "before mongoimport $MONGO_INITDB_DATABASE"
mongoimport -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD -d $MONGO_INITDB_DATABASE -c technologies_list --file /preload/technologies_list.json --jsonArray
mongoimport -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD -d $MONGO_INITDB_DATABASE -c questions --file /preload/questions.json --jsonArray