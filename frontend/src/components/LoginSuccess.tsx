import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export default function LoginSuccess() {
  const navigate = useNavigate();

  useEffect(() => {
    // Extract token from URL
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');

    if (token) {
      // Store token and redirect
      localStorage.setItem('token', token);
      navigate('/');
    } else {
      navigate('/login-error?message=Missing%20token');
    }
  }, [navigate]);

  return null;  // This component doesn't render anything
}