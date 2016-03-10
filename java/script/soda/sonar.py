from .feedback import *
from .structure import *
from .need import *
import urllib.request
import json
import hashlib

class IssueLoader(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load(self):
        pass

class LoadIssuesFromSonarServer(IssueLoader):
    def __init__(self, base_url, project):
        self._base_url = base_url
        self._project = project

    def load(self):
        base_url = CleverString(self._base_url).value
        project = CleverString(self._project).value
        print(info("loading issues of %s from %s" % (as_proper(project),as_proper(base_url))))
        response = urllib.request.urlopen('%s/api/issues/search?projectKeys=%s&ps=10' % (base_url,project))
        raw = json.loads(response.read().decode('utf-8'))
        total = int(raw['total'])
        print(info("issues count is %s" % as_sample(total)))
        issues = []
        page = 1
        while len(issues) < total:
            response = urllib.request.urlopen('%s/api/issues/search?projectKeys=%s&ps=500&p=%d' % (base_url, project, page))
            raw = json.loads(response.read().decode('utf-8'))
            issues.extend(raw['issues'])
            page += 1
            print(info("%s (%s%%) issues are loaded" % (as_sample(len(issues)), as_sample("%.4f"%(len(issues)/total*100)))))
        print(info("altogether %s issues are loaded" % as_sample(len(issues))))
        return issues

def issueIdentity(issue):
    if 'textRange' in issue:
        humanreadable = '%s %s (%d;%d):(%d;%d) "%s"' %\
                        (issue.get('rule', 'unknown'),
                         issue.get('component', 'unknown').replace(':', '').replace(issue['project'], ''),
                         issue['textRange']['startLine'],
                         issue['textRange']['endLine'],
                         issue['textRange']['startOffset'],
                         issue['textRange']['endOffset'],
                         issue.get('message', 'unknown'))
    else:
        humanreadable = '%s %s "%s"' %\
                        (issue.get('rule', 'unknown'),
                         issue.get('component', 'unknown').replace(issue['project'], ''),
                         issue.get('message', 'unknown'))
    hashed = hashlib.md5()
    hashed.update(humanreadable.encode('utf-8'))
    hexdigest = hashed.hexdigest()
    return hexdigest, humanreadable

def substractIssues(prev_issues, post_issues):
    diffs = []
    total = len(prev_issues)
    prev_percent = 0
    prev_buffer = dict((issueIdentity(issue)[0],issue) for issue in prev_issues)
    post_buffer = dict((issueIdentity(issue)[0],issue) for issue in post_issues)
    index = 0
    for prev_nid in prev_buffer:
        percent = index / total * 100
        if percent - prev_percent > 10:
            print(info("%s%% are compered." % as_sample('%.4f' % percent)))
            prev_percent = percent
        index += 1

        for post_nid in post_buffer:
            if post_nid == prev_nid:
                break
        else:
            print(info("issue %s is not present." % as_proper(prev_nid)))
            diffs.append(prev_buffer[prev_nid])
    return diffs

class DiffSonarIssues(Doable):
    def __init__(self, issueLoader_a, issuesLoader_b, ab_diff_path, ba_diff_path):
        self._issuesLoader_a = issueLoader_a
        self._issuesLoader_b = issuesLoader_b
        self._ab_diff_path = ab_diff_path
        self._ba_diff_path = ba_diff_path

    def saveIssuesTo(self, issues, log_path):
        with open(log_path, 'w') as log:
            for issue in issues:
                log.write('%s\n' % json.dumps(issue))

    def _do(self, *args, **kvargs):
        ab_diff_path = CleverString(self._ab_diff_path).value
        ba_diff_path = CleverString(self._ba_diff_path).value

        issues_a = self._issuesLoader_a.load()
        issues_b = self._issuesLoader_b.load()
        print(info("forward subtracting issues"))
        a_only = substractIssues(issues_a, issues_b)
        print(info("writing forward subtraction results to %s" % as_sample(ab_diff_path)))
        self.saveIssuesTo(a_only, ab_diff_path)
        print(info("backward subtracting issues"))
        b_only = substractIssues(issues_b, issues_a)
        print(info("writing backward subtraction results to %s" % as_sample(ba_diff_path)))
        self.saveIssuesTo(b_only, ba_diff_path)

class LoadIssuesFromLog(IssueLoader):
    def __init__(self, log_path):
        self._log_path = log_path

    def load(self):
        log_path = CleverString(self._log_path).value
        issues = []
        with open(log_path, 'r') as log:
            issues.extend([json.loads(line.strip()) for line in log])
        return issues

class AggregateIssueCount(Doable):
    def __init__(self, issueLoader, property, result_path,):
        self._issueLoader = issueLoader
        self._result_path = result_path
        self._property = property

    def _do(self, *args, **kvargs):
        issues = self._issueLoader.load()
        property = CleverString(self._property).value
        result_path = CleverString(self._result_path).value
        counts = {}
        for issue in issues:
            value = issue.get(property, 'unknown')
            if not value in counts:
                counts[value] = 0
            counts[value] += 1
        with open(result_path, 'w') as result:
            for key, count in counts.items():
                hashed = hashlib.md5()
                hashed.update(key.encode('utf-8'))
                hexdigest = hashed.hexdigest()
                result.write('%s; %s; %s\n' % (hexdigest, key, count))