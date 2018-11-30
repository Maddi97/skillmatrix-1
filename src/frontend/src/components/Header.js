import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import { AccountCircle, PowerSettingsNew } from '@material-ui/icons';

const styles = {
  root: {
    flexGrow: 1,
  },
  grow: {
    flexGrow: 1,
  },
  menuButton: {
    marginLeft: -12,
    marginRight: 20,
  },
};

function ButtonAppBar(props) {
  const {
    classes, username, logout, switchToProfile,
  } = props;

  return (
    <div className={classes.root}>
      <AppBar position="static">
        <Toolbar>
          <IconButton
            className={classes.menuButton}
            onClick={() => switchToProfile()}
            color="inherit"
            aria-label="Menu"
          >
            <AccountCircle />
          </IconButton>
          <Typography variant="h6" color="inherit" className={classes.grow}>
            {username}
          </Typography>
          <IconButton
            className={classes.menuButton}
            onClick={logout}
            color="inherit"
            aria-label="Menu"
          >
            <PowerSettingsNew />
          </IconButton>
        </Toolbar>
      </AppBar>
    </div>
  );
}

export default withStyles(styles)(ButtonAppBar);
