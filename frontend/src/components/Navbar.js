import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import Toolbar from '@material-ui/core/Toolbar';
import MenuIcon from '@material-ui/icons/Menu';
import { Link as RouterLink } from 'react-router-dom';
import Link from '@material-ui/core/Link'

// The use of React.forwardRef will no longer be required for react-router-dom v6.
// See https://github.com/ReactTraining/react-router/issues/6056
const LinkToAbout = React.forwardRef((props, ref) => (
  <RouterLink innerRef={ref} {...props} />
));

const LinkToHome = React.forwardRef((props, ref) => (
    <RouterLink innerRef={ref} to="/" {...props}/>
))


const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
    color: "#dee2e6",
  },
  buttonText: {
      color: "#dee2e6",
  }
}));

function Navbar () {
    const classes = useStyles()

    return (
        <div className={classes.root}>
            <AppBar position="static">
                <Toolbar>
                    <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
                        <MenuIcon />
                    </IconButton>
                    <Link className={classes.title} component={LinkToHome} to="/">
                        <Typography variant="h6" className={classes.title}>
                            Clean Slate Buddy
                        </Typography>
                    </Link>
                    <Button color="primary" className={classes.buttonText} component={LinkToAbout} to="/about"> 
                        About
                    </Button>
                </Toolbar>
            </AppBar>
        </div>
    )
}



export default Navbar



