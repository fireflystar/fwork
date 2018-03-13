"""fwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

import fisChannel.views
import fisChannel.doExcel
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    # url(r'^orm/', fisChannel.views.orm),
    url(r'^login/', fisChannel.views.userlogin),
    url(r'^logout/', fisChannel.views.logout),

    url(r'^sou/', fisChannel.views.sou),
    url(r'^soujinque/', fisChannel.views.soujinque),
    
    url(r'^add2db/', fisChannel.views.add2db),
    url(r'^save2db/', fisChannel.views.save2db),

]



import blog.views
urlpatterns += [
    # url(r'^blog/', blog.views.blog),
]