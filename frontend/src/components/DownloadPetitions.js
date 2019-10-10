import React, { useState } from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import Button from "@material-ui/core/Button"
import Container from "@material-ui/core/Container"
import { getPetitions } from "../actions"
import Petition from "./Petition"
import Attorneys from "./Attorneys";
/**
 * Final step in the PetitionStepper. 
 * 
 * This step is for picking which petitions to generate, and then downloading those petitions.
 * 
 * @param {} props 
 */
function DownloadPetitions(props) {
    const { attorneys, petitions, getPetitions } = props;

    const [selectedPetitions, setSelectedPetitions] = useState(petitions)

    const submitGetPetitions = (e) => {
        e.preventDefault()
        console.log("Attorney")
        console.log(attorneys[0])
        getPetitions(selectedPetitions, attorneys[0])
    }

    const downloadPetitionStyle = { margin: '15px', border: '1px solid black', borderRadius: '25px', padding: '10px', width: '950px' };
    return (
        <Container>
            <form onSubmit={submitGetPetitions}>
                <Button type="submit"> Process Petition Package </Button>
            </form>
            <div className="downloadPetition" style={downloadPetitionStyle}>
                    <Attorneys attorneys={attorneys} />
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
    attorneys: PropTypes.array.isRequired
};

function mapStateToProps(state) {
    return { 
        attorneys: state.petitionPackage.attorneysList,
        petitions: state.analysis.petitions
    };
};

function mapDispatchToProps(dispatch, ownProps) {
    return({
        getPetitions: (selectedPetitions, atty) => dispatch(getPetitions(selectedPetitions, atty))
    })
}

const DownloadPetitionsWrapper = connect(mapStateToProps, mapDispatchToProps)(DownloadPetitions);
export default DownloadPetitionsWrapper;