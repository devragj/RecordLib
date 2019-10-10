import React from "react"
import { makeStyles } from "@material-ui/core/styles"
import Card from "@material-ui/core/Card"
import CardHeader from "@material-ui/core/CardHeader"
import CardContent from "@material-ui/core/CardContent"
import Typography from "@material-ui/core/Typography"
import List from "@material-ui/core/List"
import ListItem from "@material-ui/core/ListItem"
import ListItemText from "@material-ui/core/ListItemText"

const useStyles = makeStyles(theme => {
    return({
        card: {
            minWidth: "128px",
            padding: ".5em",
            paddingBottom: "1em",
            marginBottom: "2em",
        },
        expungement: {
            border: "2px #8e24aa"
        },
        sealing: {
            border: "2px #9ccc65"
        },
        header: {
            fontSize: 18
        },
    })
})

/**
 * Display information about a petition that could be generated.
 */
function Petition(props) {
    const { petition } = props
    const classes = useStyles()
    return (
        <Card className={classes.card + " " + (petition.petition_type === "Expungement" ? classes.expungement: classes.sealing)}>
            <CardContent> 
                <Typography className={classes.header} color="textSecondary">
                    {petition.petition_type}
                </Typography>
            </CardContent>
            <CardContent> 
                <Typography variant="body2" color="textSecondary" component="p">
                    {petition.expungement_type ? petition.expungement_type : ""}
                </Typography>
                <Typography variant="body2" color="textSecondary" component="p">
                    {petition.cases.length} cases. 
                </Typography>
                <List>
                    {petition.cases.map((caseObject, idx) => {
                        return(<ListItem key={idx}> <ListItemText primary={caseObject.docket_number}> </ListItemText></ListItem>)
                    })}
                </List>
            </CardContent>
        </Card>
    )
}


export default Petition