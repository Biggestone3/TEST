import { useEffect, useState } from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Chip from '@mui/material/Chip';
import Box from '@mui/material/Box';
import FilterListIcon from '@mui/icons-material/FilterList';
import Popover from '@mui/material/Popover';
import Badge from '@mui/material/Badge';
import Tooltip from '@mui/material/Tooltip';
import IconButton from '@mui/material/IconButton';

const DOMAIN = import.meta.env.VITE_API_URL;

interface Source {
  uuid: string;
  name: string;
}

interface FilterProps {
  onFilter: (sourceIds: string[]) => void;
  onClear: () => void;
}

export default function Filter({ onFilter, onClear }: FilterProps) {
  const [availableSources, setAvailableSources] = useState<Source[]>([]);
  const [selectedSources, setSelectedSources] = useState<Source[]>([]);
  const [anchorEl, setAnchorEl] = useState<HTMLButtonElement | null>(null);

  const open = Boolean(anchorEl);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch(`${DOMAIN}/api/news/sources`);
        if (!res.ok) throw new Error('Failed to load sources');
        const { sources } = await res.json();
        setAvailableSources(sources);
      } catch (err) {
        console.error(err);
      }
    })();
  }, []);

  const handleApply = () => {
    onFilter(selectedSources.map((s) => s.uuid));
    setAnchorEl(null);
  };

  const handleClear = () => {
    setSelectedSources([]);
    onClear();
  };

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <Box sx={{ mb: 2, display: 'flex', justifyContent: 'flex-end' }}>
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
        {selectedSources.length > 0 && (
          <>
            <Box sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: 1 }}>
              {selectedSources.map((source) => (
                <Chip
                  key={source.uuid}
                  label={source.name}
                  size="small"
                  onDelete={() => {
                    setSelectedSources(selectedSources.filter(s => s.uuid !== source.uuid));
                    onFilter(selectedSources.filter(s => s.uuid !== source.uuid).map(s => s.uuid));
                  }}
                />
              ))}
              <Tooltip title="Clear all filters">
                <IconButton size="small" onClick={handleClear}>
                  <Chip label="Clear" size="small" />
                </IconButton>
              </Tooltip>
            </Box>
          </>
        )}
      </Box>

      <Tooltip title="Filter sources">
        <Badge badgeContent={selectedSources.length} color="primary" sx={{ ml: 1 }}>
          <IconButton onClick={handleClick} color={open ? 'primary' : 'default'}>
            <FilterListIcon />
          </IconButton>
        </Badge>
      </Tooltip>

      <Popover
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'right',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'right',
        }}
      >
        <Box sx={{ p: 2, width: 300 }}>
          <Autocomplete
            multiple
            disableCloseOnSelect
            options={availableSources}
            getOptionLabel={(option) => option.name}
            value={selectedSources}
            onChange={(_, value) => setSelectedSources(value as Source[])}
            renderInput={(params) => (
              <TextField
                {...params}
                label="Filter by source"
                placeholder="Select sources"
                variant="outlined"
                size="small"
              />
            )}
            sx={{ mb: 2 }}
          />

          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
            <Button
              variant="outlined"
              size="small"
              onClick={handleClose}
            >
              Cancel
            </Button>
            <Button
              variant="contained"
              size="small"
              onClick={handleApply}
              disabled={selectedSources.length === 0}
            >
              Apply
            </Button>
          </Box>
        </Box>
      </Popover>
    </Box>
  );
}