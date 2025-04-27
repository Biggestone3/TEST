import { useEffect, useState } from 'react';
import Autocomplete from '@mui/material/Autocomplete';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';

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
  };

  const handleClear = () => {
    setSelectedSources([]);
    onClear();
  };

  return (
    <Stack direction="row" spacing={2} alignItems="center" sx={{ width: '100%', mb: 3 }}>
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
          />
        )}
        sx={{ flexGrow: 1, minWidth: 240 }}
      />

      <Button
        variant="contained"
        onClick={handleApply}
        disabled={selectedSources.length === 0}
      >
        Apply
      </Button>

      <Button variant="outlined" onClick={handleClear}>
        Clear
      </Button>
    </Stack>
  );
}