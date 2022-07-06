from django.http import JsonResponse
from rest_framework.views import APIView

from .models import Tool


def get_all_tools_workflow_info():
    all_tools_info = {}

    for tool in Tool.objects.all():
        if tool.implemented:
            tool_info = {}
            tool_info["repo_link"] = tool.repo_link
            tool_info["version"] = tool.version
            tool_info["version_date"] = str(tool.versionDate)
            tool_info["input_parameters"] = tool.input_parameters
            all_tools_info[tool.name] = tool_info

    return JsonResponse(all_tools_info)


class ToolView(APIView):
    def get(self, request):
        return get_all_tools_workflow_info()
