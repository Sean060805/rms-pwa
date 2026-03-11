
document.addEventListener("DOMContentLoaded", () => {

  // ==== 🔔 TOAST POPUP (pang-notify sa taas) ====
  const toast = document.getElementById("toast");

  // Function para ipakita yung toast message
  function showToast(message, isError = false) {
    toast.textContent = message;
    toast.style.borderLeftColor = isError ? "#e53935" : "#f5b000"; // red pag error, yellow pag success
    toast.classList.remove("hidden");
    toast.classList.add("show");

    // Tatanggalin yung toast after 2.5 seconds
    setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => toast.classList.add("hidden"), 300);
    }, 2500);
  }

  // ==== 🪟 MODAL ELEMENTS (Add / Edit / View) ====
  const modalAdd = document.getElementById("modal-add");
  const modalEdit = document.getElementById("modal-edit");
  const modalView = document.getElementById("modal-view");

  // Buttons na nag-oopen/close ng modals
  const addBtn = document.getElementById("btn-add");
  const addCancel = document.getElementById("add-cancel");
  const editCancel = document.getElementById("edit-cancel");
  const viewClose = document.getElementById("view-close");

  // Yung mismong forms
  const formAdd = document.getElementById("form-add");
  const formEdit = document.getElementById("form-edit");

  // ==== ➕ ADD RECORD ====
  // Pag-click ng "Add Record" button
  addBtn.addEventListener("click", () => {
    formAdd.reset(); // linisin inputs
    modalAdd.setAttribute("aria-hidden", "false"); // ipakita modal
  });

  // Pag-cancel ng Add
  addCancel.addEventListener("click", () => {
    modalAdd.setAttribute("aria-hidden", "true");
  });

  // ==== ✏️ EDIT RECORD ====
  document.querySelectorAll(".action.edit").forEach((btn) => {
    btn.addEventListener("click", () => {
      formEdit.reset();
      modalEdit.setAttribute("aria-hidden", "false");

      // Fill up yung edit form gamit yung existing data
      formEdit.action = `/edit_record/${btn.dataset.id}`;
      document.getElementById("edit-fullname").value = btn.dataset.fullname;
      document.getElementById("edit-email").value = btn.dataset.email;
      document.getElementById("edit-username").value = btn.dataset.username;
      document.getElementById("edit-role").value = btn.dataset.role;
    });
  });

  // Pag-cancel ng Edit
  editCancel.addEventListener("click", () => {
    modalEdit.setAttribute("aria-hidden", "true");
  });

  // ==== 👁️ VIEW RECORD ====
  document.querySelectorAll(".action.view").forEach((btn) => {
    btn.addEventListener("click", () => {
      // Ipakita details sa view modal
      document.getElementById("v-fullname").textContent = btn.dataset.fullname;
      document.getElementById("v-email").textContent = btn.dataset.email;
      document.getElementById("v-username").textContent = btn.dataset.username;
      document.getElementById("v-role").textContent = btn.dataset.role;

      modalView.setAttribute("aria-hidden", "false");
    });
  });

  // Pag-close ng View modal
  viewClose.addEventListener("click", () => {
    modalView.setAttribute("aria-hidden", "true");
  });

  // ==== 🚀 ADD FORM SUBMIT ====
  formAdd.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(formAdd);
    const res = await fetch("/add_record", { method: "POST", body: formData });
    const data = await res.json();

    if (data.status === "success") {
      showToast(data.message); // success toast
      modalAdd.setAttribute("aria-hidden", "true");
      setTimeout(() => window.location.reload(), 1000);
    } else {
      showToast(data.message, true); // error toast
    }
  });

  // ==== 🧰 EDIT FORM SUBMIT ====
  formEdit.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(formEdit);
    const res = await fetch(formEdit.action, { method: "POST", body: formData });
    const data = await res.json();

    if (data.status === "success") {
      showToast(data.message);
      modalEdit.setAttribute("aria-hidden", "true");
      setTimeout(() => window.location.reload(), 1000);
    } else {
      showToast(data.message, true);
    }
  });

  // ==== ❌ DELETE RECORD ====
  document.querySelectorAll("form.inline-form").forEach((delForm) => {
    delForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      // Simple confirm box bago mag-delete
      if (!confirm("Are you sure you want to delete this record?")) return;

      const res = await fetch(delForm.action, { method: "POST" });
      const data = await res.json();

      if (data.status === "success") {
        showToast(data.message);
        setTimeout(() => window.location.reload(), 1000);
      } else {
        showToast("Something went wrong.", true);
      }
    });
  });
});
