import React, { useState } from "react"

import Container from "@material-ui/core/Container"
import Paper from "@material-ui/core/Paper"
import Typography from "@material-ui/core/Typography"
import { makeStyles } from "@material-ui/core/styles"
import TextField from "@material-ui/core/TextField"
import Button from "@material-ui/core/Button"
import CSSBaseline from "@material-ui/core/CssBaseline"

import { login } from "./api"


const useStyles = makeStyles(theme => ({
    content: {
        padding: theme.spacing(3,2)
    },
    textField: {
        marginLeft: theme.spacing(1),
        marginRight: theme.spacing(1),
        width: 200,
    }
}))

function Login() {
    
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")

    const classes = useStyles()
    
    const handleChange = (setter) => {
        return ((e) => {
            setter(e.target.value)
        })
    }

    const submitLogin = (e) => {
        e.preventDefault()
        login(username, password)
    }

    return (
        <React.Fragment>
            <CSSBaseline />
            <Container>
                <Paper className={classes.content}>
                    <Typography variant="h4">
                        Log in
                    </Typography>
                    <Typography variant="body1">
                        This is a pre-pre-alpha demo. Don't rely on this site to do anything useful yet. 
                        Its just for testing. 
                    </Typography>
                    <form id="login-form" method="post" onSubmit={submitLogin}>
                        <TextField 
                            id="id_username"
                            label="Username"
                            className={classes.textField}
                            value={username}
                            onChange = {handleChange(setUsername)}
                            />
                        <TextField 
                            type="password"
                            id="id_password"
                            label="Password"
                            className={classes.textField}
                            value={password}
                            onChange = {handleChange(setPassword)}
                            />
                        <Button type="submit">
                            Login
                        </Button>
                    </form>
                </Paper>
            </Container>
        </React.Fragment>
    )
}

export default Login;