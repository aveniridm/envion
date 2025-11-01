document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("fileInput");
  const processBtn = document.getElementById("processBtn");
  const log = document.getElementById("processLog");

  processBtn.addEventListener("click", async () => {
    const file = fileInput.files[0];
    if (!file) {
      log.textContent = "⚠️ Please select an audio file.";
      return;
    }

    log.textContent = " Processing started...";

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/process", { method: "POST", body: formData });
      const data = await res.json();
      if (data.success) {
        log.textContent = `✅ Done!\nOutput folder:\n${data.output_dir}`;
      } else {
        log.textContent = `❌ Error: ${data.error}\n${data.details || ""}`;
      }
    } catch (err) {
      log.textContent = `❌ Network error: ${err.message}`;
    }
  });
});
