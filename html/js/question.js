const elements = {
  question_vote: document.getElementById("question_vote"),
  answer: document.getElementById("answer"),
};
function question_vote(value) {
  axios.get(`/qvote/${question_id}/${value}`).then((response) => {
    elements.question_vote.innerHTML = response.data;
  });
}
function answer_vote(answer_id, value) {
  axios.get(`/avote/${answer_id}/${value}`).then((response) => {
    document.getElementById(`answer_vote_${answer_id}`).innerHTML =
      response.data;
  });
}
function answer_submit(answer) {
  axios
    .post("/answer", {
      id: -1,
      question_id: question_id,
      author: display_email.innerHTML,
      detail: tinyMCE.get("answer").getContent(),
    })
    .then((response) => {
      location.reload();
    });
}
