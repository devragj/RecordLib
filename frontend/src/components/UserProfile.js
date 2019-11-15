import React, { useEffect } from "react";
import Container from "@material-ui/core/Container"
import Paper from "@material-ui/core/Paper"
import CircularProgress from "@material-ui/core/CircularProgress"
import { connect } from "react-redux";
import {fetchUserProfile} from "../actions/user"
import { makeStyles} from "@material-ui/core/styles"
import Typography from "@material-ui/core/Typography"
import Grid from "@material-ui/core/Grid"

const useStyles = makeStyles(theme => {
    return({
        paper: {
            marginTop: theme.spacing(5),
            padding: theme.spacing(2),
        }
    })
})

function UserProfile (props) {
    const { fetchUserProfile, user } = props;
    const {username, email} = user;
    const profileLoading = !username; 
    const classes = useStyles()

    useEffect(() => {
        fetchUserProfile()
    })
    return (
        <Container>
            <Paper className={classes.paper}>
                {profileLoading ? 
                    <CircularProgress /> :
                    <Grid container spacing={3}>
                        <Grid item xs={12}>
                            <Typography variant="h3">
                               {username}
                            </Typography> 
                        </Grid>
                        <Grid item xs={6}>
                            <Typography variant="body1">
                                {email}
                            </Typography>
                        </Grid>

                    </Grid>
                }
            </Paper>
        </Container>
    )
}

function mapStateToProps(state) {
    return {
        user: state.user
    }
}

function mapDispatchToProps(dispatch) {
    return({
        fetchUserProfile: () => {dispatch(fetchUserProfile())}
    })
}


export default connect(mapStateToProps, mapDispatchToProps)(UserProfile);