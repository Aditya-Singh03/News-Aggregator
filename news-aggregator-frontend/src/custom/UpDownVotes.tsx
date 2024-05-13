function UpDownVotes(UpDownVotesProp: {
  upvotes: number;
  downvotes: number;
  width: number;
  height: number;
}) {
  const upvotes = UpDownVotesProp.upvotes;
  const downvotes = UpDownVotesProp.downvotes;
  const width = UpDownVotesProp.width;
  const height = UpDownVotesProp.height;

  return (
    <>
      {upvotes >= downvotes ? (
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox={`0 0 24 24`}
          strokeWidth={3.0}
          stroke="currentColor"
          className={`w-${width} h-${height} mt-2`}
          color="green"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M4.5 10.5 12 3m0 0 7.5 7.5M12 3v18"
          />
        </svg>
      ) : (
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          strokeWidth={3.0}
          stroke="currentColor"
          className={`w-${width} h-${height} mt-2`}
          color="red"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M19.5 13.5 12 21m0 0-7.5-7.5M12 21V3"
          />
        </svg>
      )}
    </>
  );
}

export default UpDownVotes;
