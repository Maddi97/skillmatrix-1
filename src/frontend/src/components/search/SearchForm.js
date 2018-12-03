import React from 'react';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';
import SearchField from 'components/search/SearchField';
import SearchIcon from '@material-ui/icons/Search';

const styles = theme => ({
  root: {
    width: '500px',
    margin: '2em auto',
  },
  button: {
    margin: theme.spacing.unit,
  },
  leftIcon: {
    marginRight: theme.spacing.unit,
  },
  rightIcon: {
    marginLeft: theme.spacing.unit,
  },
});

function Search(props) {
  const { classes, onSearch } = props;
  return (
    <div className={classes.root}>
      <h1>Skill Search</h1>
      <SearchField />
      <Button
        className={classes.button}
        variant="contained"
        color="primary"
        name="submit"
        onClick={() => onSearch()}
      >
        Search
        <SearchIcon className={classes.rightIcon} />
      </Button>
    </div>
  );
}

export default withStyles(styles)(Search);
