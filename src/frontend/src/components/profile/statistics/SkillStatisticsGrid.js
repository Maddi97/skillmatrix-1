// react
import React from 'react';

import Grid from '@material-ui/core/Grid';
import SimpleCard from 'components/profile/statistics/SimpleCard';
import ProfileExpansionPanel from 'components/profile/skills/ProfileExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import ExpansionPanelActions from '@material-ui/core/ExpansionPanelActions';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';

import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
  panels: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'left',
    alignItems: 'stretch',
    flexBasis: '99%',
  },
});

class SkillStatisticsPage extends React.Component {
  state = {
    expanded: null,
  };
  handleChange = panel => (event, expanded) => {
    this.setState({
      expanded: expanded ? panel : false,
    });
  };

  renderDatastructureRecursive(subcategories, index) {
    const { expanded } = this.state;
    if (subcategories === undefined) return <div />;

    const subs = subcategories.map(skill =>
      index < 5 ? (
        <ExpansionPanel expanded={expanded} onChange={this.handleChange(this.props.skill)}>
          <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
            <SimpleCard skill={skill.skillname} data={skill.milestones} />
          </ExpansionPanelSummary>
          <ExpansionPanelDetails className={this.props.classes.panels}>
            {this.renderDatastructureRecursive(skill.subcategories, index + 1)}
          </ExpansionPanelDetails>
        </ExpansionPanel>
      ) : (
        <Grid style={{ display: 'flex', flexDirection: 'row-reverse' }}>
          <SimpleCard skill={skill.skillname} data={skill.milestones} />
          {this.renderDatastructureRecursive(skill.subcategories, index)}
        </Grid>
      ),
    );

    return subs;
  }

  render() {
    const { expanded } = this.state;

    const { categories } = this.props;
    const skillItems = categories.map(skill => (
      <ExpansionPanel expanded={expanded} onChange={this.handleChange(this.props.skill)}>
        <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />}>
          {' '}
          {skill.skillname}{' '}
        </ExpansionPanelSummary>
        <ExpansionPanelDetails className={this.props.classes.panels}>
          {this.renderDatastructureRecursive(skill.subcategories, 0)}
        </ExpansionPanelDetails>
      </ExpansionPanel>
    ));

    return <div>{skillItems}</div>;
  }
}

SkillStatisticsPage.propTypes = {
  classes: PropTypes.object.isRequired,
};
export default withStyles(styles)(SkillStatisticsPage);
