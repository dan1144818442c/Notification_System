import "../style/ContinueButton.css";

export default function ContinuButton({
  setRefresh,
  ifShow,
}: {
  setRefresh: () => void;
  ifShow: boolean;
}) {
  return (
    <>
      {ifShow && (
        <button id="continu" onClick={() => setRefresh()}>
          {"אישור המשך בדיקה"}
        </button>
      )}
    </>
  );
}
