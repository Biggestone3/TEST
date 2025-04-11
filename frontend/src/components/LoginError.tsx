import { Button, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

export default function LoginError() {
  const navigate = useNavigate();
  
  return (
    <div style={{ 
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      height: '100vh',
      textAlign: 'center'
    }}>
      <Typography variant="h4" gutterBottom>
        🚨 Login Failed
      </Typography>
      <Button
        variant="contained"
        color="primary"
        onClick={() => navigate('/')}
        sx={{ mt: 2 }}
      >
        Return to Home
      </Button>
    </div>
  );
}