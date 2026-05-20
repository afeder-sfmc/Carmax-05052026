const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;
const PASSWORD = process.env.PASSWORD || 'demo';

app.use(express.urlencoded({ extended: false }));

const loginPage = (error) => `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MCA Lean Deployment — Login</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #001333; display: flex; align-items: center; justify-content: center; min-height: 100vh; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .card { background: white; border-radius: 16px; padding: 40px; width: 100%; max-width: 380px; }
    .logo { color: #001333; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 8px; }
    h1 { color: #001333; font-size: 22px; font-weight: 900; margin-bottom: 28px; line-height: 1.3; }
    label { display: block; font-size: 12px; font-weight: 700; color: #646E82; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px; }
    input[type=password] { width: 100%; border: 1.5px solid #CCD0D6; border-radius: 8px; padding: 10px 14px; font-size: 15px; outline: none; transition: border-color 0.2s; }
    input[type=password]:focus { border-color: #005DFF; }
    button { width: 100%; margin-top: 18px; background: #FFD100; color: #001333; font-weight: 700; font-size: 14px; border: none; border-radius: 10px; padding: 12px; cursor: pointer; }
    button:hover { background: #FEC000; }
    .error { color: #D32F2F; font-size: 13px; margin-top: 12px; }
  </style>
</head>
<body>
  <div class="card">
    <p class="logo">CarMax × Salesforce</p>
    <h1>MCA Lean Deployment Model</h1>
    <form method="POST" action="/login">
      <label for="password">Password</label>
      <input type="password" id="password" name="password" autofocus autocomplete="current-password" />
      <button type="submit">View Presentation</button>
      ${error ? '<p class="error">Incorrect password. Please try again.</p>' : ''}
    </form>
  </div>
</body>
</html>`;

// Simple session via signed cookie
const COOKIE_NAME = 'mca_auth';
const COOKIE_VALUE = 'authenticated';

app.get('/login', (req, res) => res.send(loginPage(false)));

app.post('/login', (req, res) => {
  if (req.body.password === PASSWORD) {
    res.setHeader('Set-Cookie', `${COOKIE_NAME}=${COOKIE_VALUE}; HttpOnly; Path=/; SameSite=Strict; Max-Age=86400`);
    res.redirect('/');
  } else {
    res.send(loginPage(true));
  }
});

app.get('/logout', (req, res) => {
  res.setHeader('Set-Cookie', `${COOKIE_NAME}=; HttpOnly; Path=/; Max-Age=0`);
  res.redirect('/login');
});

function requireAuth(req, res, next) {
  const cookies = Object.fromEntries(
    (req.headers.cookie || '').split(';').map(c => c.trim().split('=').map(decodeURIComponent))
  );
  if (cookies[COOKIE_NAME] === COOKIE_VALUE) return next();
  res.redirect('/login');
}

app.get('/', requireAuth, (req, res) => {
  res.sendFile(path.join(__dirname, 'mca-lean-deployment.html'));
});

app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
