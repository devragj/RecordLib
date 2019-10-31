import React, { useState } from "react";
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import Button from "@material-ui/core/Button"
import Container from "@material-ui/core/Container"
import { fetchPetitions } from "../actions"
import Petition from "./Petition"
import AttorneyHolder from "./AttorneyHolder";
import AddAttorney from "./AddAttorney"
import ServiceAgencyList from "./ServiceAgencyList"
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

    const [isReadyToSubmit, setIsReadyToSubmit] = useState(false)

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
                <h4> There are a few other pieces of information you need to generate petitions. </h4>

                <Button type="submit"> Process Petition Package </Button>
                <h5> Attorney whose name will appear on petitions </h5>
                <div className="downloadPetition" style={downloadPetitionStyle}>
                        {
                            attorney.hasOwnProperty("full_name") ? 
                            <AttorneyHolder attorney={attorney} /> :
                            <AddAttorney />
                        }
                </div>
                <ServiceAgencyList />
            </form>
            <div>
                {
                    petitions.length > 0 ?
                        petitions.map((petition, idx) => {
                        return(<Petition key={idx} petition={petition}></Petition>)
                    }) :
                    <p> There are no petitions to display yet. Have you conducted an analysis yet? </p>
                }
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
        petitions: state.analysis.petitions || [],
        petitionPackage: state.petitionPackage,
    };
};

function mapDispatchToProps(dispatch, ownProps) {
    return({
        getPetitions: (selectedPetitions, atty) => dispatch(fetchPetitions(selectedPetitions, atty))
    })
}

const DownloadPetitionsWrapper = connect(mapStateToProps, mapDispatchToProps)(DownloadPetitions);
export default DownloadPetitionsWrapper;