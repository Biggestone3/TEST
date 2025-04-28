import * as React from 'react';
import { styled, alpha } from '@mui/material/styles';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import InputBase from '@mui/material/InputBase';
import SearchIcon from '@mui/icons-material/Search';
import LanguageIcon from '@mui/icons-material/Language';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Button from '@mui/material/Button';
import GoogleIcon from '@mui/icons-material/Google';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';
import { useGoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';

const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.black, 0.05),
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.black, 0.08),
  },
  width: '100%',
  [theme.breakpoints.up('sm')]: {
    width: 'auto',
  },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  width: '100%',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    transition: theme.transitions.create('width'),
  },
}));

interface SearchAppBarProps {
  language: 'en' | 'ar';
  setLanguage: React.Dispatch<React.SetStateAction<'en' | 'ar'>>;
}

export default function SearchAppBar({ language, setLanguage }: SearchAppBarProps) {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const [errorMessage, setErrorMessage] = React.useState('');
  const [openError, setOpenError] = React.useState(false);
  const isRTL = language === 'ar';
  const navigate = useNavigate();

  const handleCloseError = () => setOpenError(false);

  const handleGoogleLogin = useGoogleLogin({
    flow: 'auth-code',
    onSuccess: async (codeResponse) => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/api/auth/google/callback`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: codeResponse.code }),
          }
        );

        const responseText = await response.text();

        if (!response.ok) {
          throw new Error(responseText || 'Authentication failed');
        }

        let data;
        try {
          data = JSON.parse(responseText);
        } catch (err) {
          console.error('Failed to parse response as JSON:', err);
          throw new Error('Invalid server response format');
        }

        localStorage.setItem('authToken', data.access_token);
        navigate('/');

      } catch (error) {
        const message = error instanceof Error ? error.message : 'Login failed';
        console.error('Login error:', message);
        setErrorMessage(message);
        setOpenError(true);
      }
    },
    onError: (error) => {
      const message = error.error_description || 'Google login failed';
      console.error('Google auth error:', message);
      setErrorMessage(message);
      setOpenError(true);
    }
  });

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    navigate('/');
  };

  const handleRefresh = () => {
    navigate(0);
  };

  return (
    <>
      <AppBar position="fixed" sx={{
        width: '100%',
        backgroundColor: '#ffffff',
        direction: isRTL ? 'rtl' : 'ltr'
      }}>
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <IconButton
              edge="start"
              color="inherit"
              aria-label="language"
              onClick={(e) => setAnchorEl(e.currentTarget)}
              sx={{ color: 'black' }}
            >
              <LanguageIcon />
            </IconButton>
            {!localStorage.getItem('authToken') ? (
              <Button
                variant="outlined"
                startIcon={<GoogleIcon />}
                sx={{ color: '#4285F4', borderColor: '#4285F4', '&:hover': { borderColor: '#357ABD' } }}
                onClick={() => handleGoogleLogin()}
              >
                {isRTL ? 'تسجيل الدخول' : 'Login'}
              </Button>
            ) : (
              <Button
                variant="outlined"
                sx={{ color: 'black', borderColor: 'black' }}
                onClick={handleLogout}
              >
                {isRTL ? 'تسجيل الخروج' : 'Logout'}
              </Button>
            )}

            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={() => setAnchorEl(null)}
            >
              <MenuItem onClick={() => setLanguage('en')}>English</MenuItem>
              <MenuItem onClick={() => setLanguage('ar')}>عربي</MenuItem>
            </Menu>
          </Box>

          <Typography
            variant="h6"
            component="div"
            onClick={handleRefresh}
            sx={{
              position: 'absolute',
              left: '50%',
              transform: 'translateX(-50%)',
              color: 'black',
              cursor: 'pointer',
              '&:hover': {
                textDecoration: 'underline'
              }
            }}
          >
            {isRTL ? 'الأخبار' : 'NEWS'}
          </Typography>

          <Search sx={{
            width: isRTL ? 100 : 100,
            marginLeft: isRTL ? 1 : 0,
            marginRight: isRTL ? 0 : 1
          }}>
            <SearchIconWrapper sx={{
              [isRTL ? 'right' : 'left']: 0
            }}>
              <SearchIcon sx={{ color: 'text.secondary' }} />
            </SearchIconWrapper>
            <StyledInputBase
              placeholder={isRTL ? 'بحث...' : 'Search...'}
              inputProps={{ 'aria-label': 'search' }}
              sx={{
                '& .MuiInputBase-input': {
                  [isRTL ? 'paddingRight' : 'paddingLeft']: `calc(1em + ${48}px)`,
                }
              }}
            />
          </Search>
        </Toolbar>
      </AppBar>

      <Snackbar
        open={openError}
        autoHideDuration={6000}
        onClose={handleCloseError}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseError} severity="error" sx={{ width: '100%' }}>
          {errorMessage}
        </Alert>
      </Snackbar>
    </>
  );
}