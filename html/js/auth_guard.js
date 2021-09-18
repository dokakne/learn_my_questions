var current_user = { id: -1, email: "", password: "", name: "" };

function auth_guard(callback) {
  axios
    .get("/user", {
      headers: { Authorization: `Bearer ${Cookies.get("email")}` },
    })
    .then((response) => {
      if (response.data.user) {
        current_user = response.data.user;
        profile.innerHTML = current_user.name;
        callback();
      } else {
        window.location.href = "/login";
      }
    })
    .catch((error) => {
      window.location.href = "/login";
    });
}
