I have not got far into installing them for offline use, but here is some advice:

https://docs.openvino.ai/2025/get-started/install-openvino.html?PACKAGE=OPENVINO_BASE&VERSION=v_2025_4_0&OP_SYSTEM=LINUX&DISTRIBUTION=PIP - OpenVINO is Intel's standard.
- I managed to get it into my APT list with CLI, then install with standard installer.

https://onnxruntime.ai/getting-started
- Interactive piece, which asks all the questions about what kind of controller software or library you want;
- then gives you an instruction, how to install it.

What you need is
- Alt.: ONNX driver to inference with ONNX models, https://onnxruntime.ai/docs/install/.
- Alt.: OpenVINO has converter from ONNX to IR, it's own format, to use it's inference.

There are models like Stable Diffusion you need to install for image generation.

This is intel-basic way to do it, which might work on other systems as well; but it meets my reqs now in this:
- I do have intel. Despite liking AMD and Radeon.
- It has good installer, which does not bring you into consciousness of versions of pip and linux packages, understanding of bash scripts or creating virtual environments.
  - Here we have ecosystem of tens of AI tools:
    - We might want to give an installation instruction to grandmother.
    - We might want to create software, which installs and uses something automatically.
   
So while I have before suggested a library here, then replaced it later; but still I gave you this notice.
- I now really need offline, small model for image generation, because I really do have some goals like writing a simple script to autogenerate images and design.
