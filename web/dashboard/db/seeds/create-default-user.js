const bcrypt = require('bcrypt');

exports.seed = async function seed(knex) {
  const hashedPass = await bcrypt.hash('1234', 5);
  await knex('users').insert({
    name: 'admin admin',
    email: 'test@gmail.com',
    password: hashedPass,
    created_at: new Date(),
    updated_at: new Date(),
    email_verified_at: new Date(),
  });
};
