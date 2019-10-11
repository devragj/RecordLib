import React, { useState } from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import Button from "@material-ui/core/Button"
import Container from "@material-ui/core/Container"
import { getPetitions } from "../actions"
import Petition from "./Petition"
import AttorneyHolder from "./AttorneyHolder";
import AddAttorney from "./AddAttorney"

/**
 * Final step in the PetitionStepper. 
 * 
 * This step is for picking which petitions to generate, and then downloading those petitions.
 * 
 * @param {} props 
 */
function DownloadPetitions(props) {
    const { attorney, petitions, getPetitions, petitionPackage } = props;

    const [selectedPetitions, setSelectedPetitions] = useState(petitions)

    const submitGetPetitions = (e) => {
        e.preventDefault()
        console.log("Attorney")
        console.log(attorney)
        getPetitions(selectedPetitions, attorney)
    }

    const downloadPetitionStyle = { margin: '15px', border: '1px solid black', borderRadius: '25px', padding: '10px', width: '950px' };
    return (
        <Container>
            {
                petitionPackage.hasOwnProperty("path") ? 
                <a href={petitionPackage.path} download> Download the petition package </a> :
                ""
            }
            <form onSubmit={submitGetPetitions}>
                <Button type="submit"> Process Petition Package </Button>
            </form>
            <div className="downloadPetition" style={downloadPetitionStyle}>
                    {
                        attorney.hasOwnProperty("full_name") ? 
                        <AttorneyHolder attorney={attorney} /> :
                        <AddAttorney />
                    }
            </div>
            <div>
                {petitions.map((petition, idx) => {
                    return(<Petition key={idx} petition={petition}></Petition>)
                })}
            </div>
        </Container>
    );
};

DownloadPetitions.propTypes = {
    attorney: PropTypes.object.isRequired
};

function mapStateToProps(state) {
    return { 
        attorney: state.attorney,
        petitions: state.analysis.petitions,
        petitionPackage: state.petitionPackage,
    };
};

function mapDispatchToProps(dispatch, ownProps) {
    return({
        getPetitions: (selectedPetitions, atty) => dispatch(getPetitions(selectedPetitions, atty))
    })
}

const DownloadPetitionsWrapper = connect(mapStateToProps, mapDispatchToProps)(DownloadPetitions);
export default DownloadPetitionsWrapper;