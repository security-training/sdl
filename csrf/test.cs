using System.Web.UI;

String serializedProperties="TBZWD78zhS+ak4NadXH9jbcTIvAv3bgVYfOK8hP9JcvwD+m8kkcCy4R6TwUwCYRUmxJzwMCkAoejBxLrnpz0v+3a4x/jq9oLuvKsHTQlNKVX5jrTesoGOUScyAVpphfNpkOk0snbS6X1SLnEQ3fuH9X9HmCbEG+0ZajE35fIYFXBsvlcnwI6EgfmSVx8qqCns0vGawapIBb41scFfg5ErvoJOSXk2eynwSv+J3qrlCpEVu4EaCk+rUfZHpfPlho1lje1/vQ4w5hBFN1AGqT3JzX9efNWrmuMJRQ/2WNzdhfqGF4oM+yXWHzlRpSYWlIbHg22lhWLaPZreg3CIQFXoAQKg5QXegRRM2jGfKZUozU="

private ICollection LoadControlProperties (string serializedProperties) {

    ICollection controlProperties = null;

    // Create an ObjectStateFormatter to deserialize the properties.
    ObjectStateFormatter formatter = new ObjectStateFormatter();

    // Call the Deserialize method.
    controlProperties = (ArrayList) formatter.Deserialize(serializedProperties);

    return controlProperties;
}