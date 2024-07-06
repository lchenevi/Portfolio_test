// Initialize Supabase
const supabaseUrl = 'https://zysgqekxxqexyptfsdye.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp5c2dxZWt4eHFleHlwdGZzZHllIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTkwNjA4MzAsImV4cCI6MjAzNDYzNjgzMH0.laJ4M8oAS7MDbNIM1_LFYLFf9wiQBnUNXKn_uHjzmcg';
const supabase = supabase.createClient(supabaseUrl, supabaseKey);

// Handle registration form submission
document.getElementById('register-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;

    const { user, error } = await supabase.auth.signUp({
        email: email,
        password: password,
    });

    if (error) {
        console.error('Error registering:', error.message);
    } else {
        console.log('User registered:', user);
        alert('Registration successful! Please check your email to confirm.');
    }
});

// Handle login form submission
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    const { user, session, error } = await supabase.auth.signIn({
        email: email,
        password: password,
    });

    if (error) {
        console.error('Error logging in:', error.message);
    } else {
        console.log('User logged in:', user);
        alert('Login successful!');
        window.location.href = 'dashboard.html'; // Redirect to your dashboard page
    }
});
