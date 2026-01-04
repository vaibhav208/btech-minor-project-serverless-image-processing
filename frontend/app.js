// ===== CONFIGURATION =====
const REGION = "us-east-1";
const IDENTITY_POOL_ID = "us-east-1:a3198016-dfe4-4a5d-838a-569e3ddd0b6e";
const INPUT_BUCKET = "serverless-image-processing-input-aa42ab4a";
// =========================

// AWS SDK config
AWS.config.region = REGION;

AWS.config.credentials = new AWS.CognitoIdentityCredentials({
  IdentityPoolId: IDENTITY_POOL_ID,
});

const s3 = new AWS.S3({
  apiVersion: "2006-03-01",
  params: { Bucket: INPUT_BUCKET },
});

// ===== IMAGE PREVIEW =====
document
  .getElementById("fileInput")
  .addEventListener("change", function (event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function (e) {
      document.getElementById("preview").src = e.target.result;
    };
    reader.readAsDataURL(file);
  });

// ===== UPLOAD FUNCTION =====
function uploadImage() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select an image first");
    return;
  }

  const fileName = Date.now() + "-" + file.name;
  document.getElementById("status").innerText = "Authenticating...";

  // 🔴 CRITICAL FIX: fetch temporary credentials
  AWS.config.credentials.get(function (err) {
    if (err) {
      console.error("Cognito error:", err);
      document.getElementById("status").innerText = "Authentication failed";
      return;
    }

    document.getElementById("status").innerText = "Uploading image...";

    s3.upload(
      {
        Key: fileName,
        Body: file,
        ContentType: file.type,
      },
      function (err, data) {
        if (err) {
          console.error("Upload error:", err);
          document.getElementById("status").innerText = "Upload failed";
          return;
        }

        document.getElementById("status").innerText =
          "Upload successful. Processing started...";

        const outputBucket = INPUT_BUCKET.replace("input", "output");

        document.getElementById("resizedLink").href =
          `https://${outputBucket}.s3.amazonaws.com/resized/${fileName}`;

        document.getElementById("thumbnailLink").href =
          `https://${outputBucket}.s3.amazonaws.com/thumbnail/${fileName}`;
      },
    );
  });
}
