import { TOPICS } from "./utils/constants";
import { useState } from "react";
import { BACKEND_URL } from "./utils/constants";
import { PreferencesInfo } from "./types";
import { AlertDestructive } from "./custom/Alert";

function Preferences(PreferencesProps: PreferencesInfo) {
  const authToken = PreferencesProps.authToken;
  const setFirstTimeUser = PreferencesProps.setFirstTimeUser;
  const [currentTopics, setCurrentTopics] = useState<string[]>([]);
  const [showError, setShowError] = useState(false);

  /*
background-color: #8BC6EC;
background-image: linear-gradient(135deg, #8BC6EC 0%, #9599E2 100%);

*/

  const handleTopicSelection = (event: React.SyntheticEvent, topic: string) => {
    event.preventDefault();
    if (currentTopics.includes(topic)) {
      console.log("trying to remove");
      setCurrentTopics(currentTopics.filter((t) => t !== topic));
    } else {
      setCurrentTopics([...currentTopics, topic]);
      console.log("added");
    }
  };

  const handleSubmit = (event: React.SyntheticEvent) => {
    event.preventDefault();
    if (currentTopics.length < 5) {
      setShowError(true);
    } else {
      fetch(`${BACKEND_URL}/user/add-preferences`, {
        method: "POST",
        body: JSON.stringify({ preferences: currentTopics }),
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${authToken}`,
        },
      })
        .then(() => setFirstTimeUser(false))
        .catch((err) => console.log(err));
    }
  };

  return (
    <>
      <div className=" w-screen h-screen flex items-center bg-gradient-to-b from-[#161616] to-slate-900">
        <div className="overflow-y-scroll overflow-x-hidden top-5 h-5/6 w-4/5 relative mx-auto bottom-10 bg-[#161616] border-2 border-slate-200 text-white rounded-md">
          <div className="font-anton m-10">
            <div className="flex justify-between">
              <h1 className="font-anton text-5xl mb-5">Hello!</h1>
              <div className="font-sans">
                {showError ? (
                  <AlertDestructive
                    error="Invalid Selection"
                    message="Please pick at least 5 topics"
                  />
                ) : (
                  <div className="p-[41px]"></div>
                )}
              </div>
            </div>
            <h1 className="font-anton text-3xl">
              Select at least 5 topics you're interested in.
            </h1>
          </div>
          <div className=" flex flex-wrap m-4 ">
            {TOPICS.map((topic) => (
              <div
                id={topic}
                className={`${
                  !currentTopics.includes(topic)
                    ? "bg-[#161616] border-[1px] border-white hover:bg-[#222222]"
                    : "bg-slate-300 text-black border-[1px] hover:bg-slate-400"
                } flex flex-col w-fit p-2 h-14 text-center justify-center align-middle rounded-full m-3 font-sans hover:cursor-pointer`}
                onClick={(e) => handleTopicSelection(e, topic)}
              >
                <div className="m-2">{topic} </div>
              </div>
            ))}
          </div>
          <div className="flex absolute bottom-0 left-[calc(50%-3.875rem)]">
            <button
              className=" bg-white hover:bg-slate-300 text-black w-24 m-5 p-2 text-xl rounded-lg font-anton md:tracking-wide"
              onClick={handleSubmit}
            >
             Continue 
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

export default Preferences;
