%{?scl:%scl_package osgi-annotation}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

Name:    %{?scl_prefix}osgi-annotation
Version: 6.0.0
Release: 2.1%{?dist}
Summary: Annotations for use in compiling OSGi bundles

License: ASL 2.0
URL:     http://www.osgi.org/
# Upstream project is behind an account registration system with no anonymous
# read access, so we download the source from maven central instead
Source0: http://repo1.maven.org/maven2/org/osgi/osgi.annotation/%{version}/osgi.annotation-%{version}-sources.jar
Source1: http://repo1.maven.org/maven2/org/osgi/osgi.annotation/%{version}/osgi.annotation-%{version}.pom

BuildArch:     noarch

BuildRequires: %{?scl_prefix_java_common}maven-local

%description
Annotations for use in compiling OSGi bundles. This package is not normally
needed at run-time.

%package javadoc
Summary: API documentation for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -n %{pkg_name}-%{version} -c -q

mkdir -p src/main/resources && mv about.html src/main/resources
mkdir -p src/main/java && mv org src/main/java
cp -p %{SOURCE1} pom.xml

# Ensure OSGi metadata is generated
%pom_xpath_inject pom:project "
  <packaging>bundle</packaging>
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.felix</groupId>
        <artifactId>maven-bundle-plugin</artifactId>
        <extensions>true</extensions>
        <configuration>
          <instructions>
            <Bundle-Name>\${project.artifactId}</Bundle-Name>
            <Bundle-SymbolicName>\${project.artifactId}</Bundle-SymbolicName>
          </instructions>
        </configuration>
      </plugin>
    </plugins>
  </build>"

# Known by two names in maven central, so add an alias for the older name
%mvn_alias org.osgi:osgi.annotation org.osgi:org.osgi.annotation
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%doc LICENSE
%dir %{_javadir}/osgi-annotation
%dir %{_mavenpomdir}/osgi-annotation

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Tue Jun 23 2015 Mat Booth <mat.booth@redhat.com> - 6.0.0-2.1
- Import latest from Fedora

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 26 2015 Mat Booth <mat.booth@redhat.com> - 6.0.0-1
- Initial package