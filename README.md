<div align="center" style="font-family: 'Segoe UI', sans-serif">
  <style>
    .fade-in {
      animation: fadeIn 2s;
    }
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    .underline {
      border-bottom: 1px solid #ddd;
      padding-bottom: 3px;
    }
  </style>

  <h1 class="fade-in underline">RESEARCHER</h1>
  
  <p style="margin-top: 20px; letter-spacing: 1px">
  SYSTEMS · NETWORKS · SECURITY
  </p>

  <div style="
    margin-top: 30px;
    font-size: 0.9em;
    color: #666;
    font-style: italic;
  ">
    <p>// Last active: <span id="date"></span></p>
  </div>
</div>

<script>
  document.getElementById('date').innerText = new Date().toISOString().split('T')[0];
</script>
