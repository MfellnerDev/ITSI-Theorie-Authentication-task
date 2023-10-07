const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const session = require('express-session');
const bcrypt = require('bcrypt');

const app = express();

// Connect to MongoDB
mongoose.connect('mongodb://127.0.0.1:27017/users', {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

// User schema and model
const userSchema = new mongoose.Schema({
    username: String,
    password: String,
    color: String,
});

const User = mongoose.model('User', userSchema);

app.set('view engine', 'pug');
app.use(bodyParser.urlencoded({ extended: true }));
app.use(session({ secret: '@sbN$IHa.MK5j8]w;J>vZXKWS|6v,m', resave: false, saveUninitialized: true }));

// app index route
app.get('/', (req, res) => {
    res.render('index');
})

// Route for registering a new user
app.get('/register', (req, res) => {
    res.render('register');
});

app.post('/register', async (req, res) => {
    const { username, password, color } = req.body;

    try {
        const hashedPassword = await bcrypt.hash(password, 10);
        const user = new User({
            username,
            password: hashedPassword,
            color,
        });
        await user.save();
        res.redirect('/login');
    } catch (error) {
        res.send('Error registering user.');
    }
});

// Route for user login
app.get('/login', (req, res) => {
    res.render('login');
});

app.post('/login', async (req, res) => {
    const { username, password } = req.body;

    try {
        const user = await User.findOne({ username });

        if (!user || !(await bcrypt.compare(password, user.password))) {
            res.send('Invalid username or password.');
        } else {
            req.session.user = user;
            res.redirect('/dashboard');
        }
    } catch (error) {
        res.send('Error logging in.');
    }
});

// Route for user dashboard
app.get('/dashboard', (req, res) => {
    if (!req.session.user) {
        return res.redirect('/login');
    }

    res.render('dashboard', { user: req.session.user });
});

app.post('/change-color', async (req, res) => {
    if (!req.session.user) {
        return res.redirect('/login');
    }

    const { newColor } = req.body;
    const userId = req.session.user._id;

    try {
        await User.findByIdAndUpdate(userId, { $set: { color: newColor } });

        req.session.user.color = newColor;

        res.redirect('/dashboard');
    } catch (error) {
        res.send('Error changing color.');
    }
});

// start app
app.listen(3000, () => {
    console.log('Server started on http://localhost:3000');
});
