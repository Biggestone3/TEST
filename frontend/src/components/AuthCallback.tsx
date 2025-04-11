import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const AuthCallback = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const handleAuth = async () => {
            try {
                const params = new URLSearchParams(window.location.search);
                const code = params.get('code');

                if (!code) throw new Error('Missing authorization code');

                const response = await fetch(
                    `${import.meta.env.VITE_API_URL}/auth/google/callback`,
                    {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ code }),
                    }
                );

                const responseText = await response.text();
                if (!response.ok) throw new Error(responseText || 'Authentication failed');

                const data = JSON.parse(responseText);
                localStorage.setItem('authToken', data.access_token);
                navigate('/');

            } catch (error) {
                const message = error instanceof Error ? error.message : 'Login failed';
                navigate(`/login-error?message=${encodeURIComponent(message)}`, {
                    replace: true
                });
            }
        };

        handleAuth();
    }, [navigate]);

    return <div>Processing authentication...</div>;
};

export default AuthCallback;