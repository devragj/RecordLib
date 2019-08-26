import React from "react";

function Defendant(props) {
    const defendantStyle = {display: 'grid', gridTemplateColumns: '250px 250px', margin: '15px', border: '1px solid black', borderRadius: '5px', padding: '10px', width: '900px'};
    const name = props.first_name + " " + props.last_name;
    return (
        <div className="defendant" style={defendantStyle}>
            <div>{name}</div>
            <div></div>
            <div>DOB: {props.date_of_birth}</div>
            <div>Deceased Date: {props.date_of_death}</div>
        </div>
    );
}

export default Defendant;