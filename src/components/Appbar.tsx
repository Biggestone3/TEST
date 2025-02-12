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
  const isRTL = language === 'ar';

  return (
    <AppBar position="fixed" sx={{ 
      width: '100%', 
      backgroundColor: '#ffffff',
      direction: isRTL ? 'rtl' : 'ltr'
    }}>
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="language"
            onClick={(e) => setAnchorEl(e.currentTarget)}
            sx={{ color: 'black' }}
          >
            <LanguageIcon />
          </IconButton>

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
          sx={{ 
            position: 'absolute',
            left: '50%',
            transform: 'translateX(-50%)',
            color: 'black'
          }}
        >
          {isRTL ? 'الأخبار' : 'NEWS'}
        </Typography>

        <Search sx={{ 
          width: isRTL ? 300 : 300, // Consistent width
          marginLeft: isRTL ? 2 : 0,
          marginRight: isRTL ? 0 : 2
        }}>
          <SearchIconWrapper sx={{ 
            [isRTL ? 'right' : 'left']: 0 // Dynamic positioning
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
  );
}