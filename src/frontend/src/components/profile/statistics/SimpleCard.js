import React from 'react';
import PropTypes from 'prop-types';

import { withStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import ButtonBase from '@material-ui/core/ButtonBase';
import Dialog from '@material-ui/core/Dialog';
import Slide from '@material-ui/core/Slide';
import DialogActions from '@material-ui/core/DialogActions';
import Button from '@material-ui/core/Button';

import Chart from './Chart';

const styles = theme => ({
  root: {
    height: 180,
  },
  appBar: {
    position: 'relative',
  },
  flex: {
    flex: 1,
  },
  container: {
    display: 'flex',
  },

  card: {
    minWidth: 150,
  },
});

export class ClickableChart extends React.Component {
  state = {
    open: false,
  };

  handleClickOpen = () => {
    this.setState({ open: true });
  };

  handleClose = () => {
    this.setState({ open: false });
  };

  render() {
    const { classes } = this.props;

    const milestones = Object.keys(classes.data).map(key => (
      <Typography key={key}>
        Datum: {classes.data[key].date}, Level update auf: {classes.data[key].level} Beschreibung:{' '}
        {classes.data[key].comment}
      </Typography>
    ));
    return (
      <div>
        <Card className={classes.card}>
          <ButtonBase className={this.props.classes.cardAction} onClick={this.handleClickOpen}>
            <CardContent>
              <Chart //render small chart at the Card
                height={200}
                width={300}
                display={false}
                skill={this.props.skill}
                data={classes.data}
                enabledZoom={false}
              />
            </CardContent>
          </ButtonBase>
        </Card>
        <Dialog open={this.state.open} onClose={this.handleClose} TransitionComponent={Transition}>
          <Typography variant="h5" component="h2">
            <Card>
              <CardContent>
                <Typography variant="h5" component="h2">
                  <Chart //render small chart at the Card
                    height={400}
                    width={800}
                    display={true}
                    skill={this.props.skill}
                    data={classes.data}
                    enabledZoom={true}
                  />
                </Typography>
                Milestones: {milestones}
              </CardContent>
            </Card>
          </Typography>
          <DialogActions>
            <Button onClick={this.handleClose} color="primary">
              Cancel
            </Button>
          </DialogActions>
        </Dialog>
        <div />
      </div>
    );
  }
}

//SimpleCard renders one Clickable Chart
function SimpleCard(props) {
  return <ClickableChart skill={props.skill} classes={props} />;
}
function Transition(props) {
  return <Slide direction="up" {...props} />;
}

SimpleCard.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(SimpleCard);